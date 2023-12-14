''' Helper functions for Client '''

def myprint(obj, lvl = 0): 
    ''' Temporary helper to parse Client responses '''
    obj_type = str(type(obj))
    indent = ' ' * (lvl * 4)

    # Bool or String
    if obj_type == "<class 'bool'>" or obj_type == "<class 'str'>":
        print(f'{indent}{obj}')

    # List
    elif obj_type == "<class 'list'>":
        print('[')
        for entry in obj:
            print(f'{indent}{myprint(entry, lvl+1)}', end='')
            if entry != obj[-1]:
                print(',')
        print(f'{indent}]')

    # Dictionary
    elif obj_type == "<class 'dict'>":
        print('{')
        for k, v in obj.items():
            print(f'{indent}{k}: {myprint(v, lvl+1)}', end='')
            print(',')
        print(f'{indent}' + '}')

    # None
    elif obj_type == "<class 'NoneType'>":
        print('None')
