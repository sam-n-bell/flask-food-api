from typing import List


def convert_single_cursor_to_dict(cursor, field_names: List[str]):
    if cursor is None or len(field_names) == 0:
        return None
    response = {}
    for field in field_names:
        try:
            if field == '_id':
                response[field] = str(cursor[field])
            else:
                response[field] = cursor[field]
        except Exception as e:
            print(f'Error converting to dict for field {field}. Message = {e}')
    return response

def convert_cursor_to_list_of_dicts(cursor, field_names: List[str]):
    if cursor is None or len(field_names) == 0:
        return None
    response = []
    for item in cursor:
        current_item = {}
        for field in field_names:
            try:
                if field == '_id':
                    current_item[field] = str(item[field])
                else:
                    current_item[field] = item[field]
                response.append(current_item)
            except Exception as e:
                print(f'Error converting to dict for field {field}. Message = {e}')
    return response