# /config/python_scripts/set_state.py
# entity_id = data.get("entity_id")
# states = data.get("state")

# if entity_id:
#     hass.states.set(entity_id, states)

entity_id = data.get("entity_id")
new_state = data.get("state")

if entity_id:
    # 1. Считываем объект из Home Assistant, если он уже существует
    current_object = hass.states.get(entity_id)
    
    if current_object:
        # Если объект есть, берем его текущие атрибуты и статус
        state_value = new_state if new_state is not None else current_object.state
        # ИСПРАВЛЕНО: используем .copy() вместо dict()
        attributes = current_object.attributes.copy()
    else:
        # Если объекта еще нет в системе (создается впервые)
        state_value = new_state if new_state is not None else "unknown"
        attributes = {}

    # 2. Дописываем все новые атрибуты, переданные через data (кроме служебных)
    for key, value in data.items():
        if key not in ["entity_id", "state"]:
            attributes[key] = value

    # 3. Сохраняем обновленный объект назад в систему
    hass.states.set(entity_id, state_value, attributes)


