import json
import uuid
import re
import copy


class WAGA_JSON_VALIDATOR_1_0_5:
    """
    Class representing JSON validator for WAGA software according to API version 1.0.5

    Methods:
    -----------
    validate_json_file(json_file)
        Validates given json file. Provides a JSON file with conflicts if they are present.
        Output --> (True, None) or (False, {json_str_with_details})
    validate_json_str(json_str)
        Validates given json object in string format. Provides a JSON file with conflicts if they are present.
        Output --> (True, None) or (False, {json_str_with_details})
    """

    JSON_SCHEMA = {
        1: {"uuid": "UUID"},
        2: {"deviceId": "UUID"},
        3: {"eventDeviceId": "str"},
        4: {"datetime": "ISO8601"},
        6: {
            "origin": {
                "uuid": "UUID",
                "__name": "str",
                "__address": "str",
                "__serial": "str",
                "location": {"latitude": "WGS84", "longitude": "WGS84"},
            }
        },
        8: {
            "measurements": [
                "key-value",
                {
                    "values": [
                        ("speed-main", "+int"),
                        ("weight-full", "+int"),
                        ("length", "+int"),
                        ("width", "+int"),
                        ("height", "+int"),
                        ("axlecount", "+int"),
                    ],
                    "non-mandatory values": [
                        ("road-temperature", "int"),
                        ("air-temperature", "int"),
                    ],
                    "dependent-values": [
                        ("axlecount", 0, "axleload-N", "N", "+int"),
                        ("axlecount", -1, "axledistance-N", "N", "+int"),
                        ("axlecount", 0, "wheeltype-N", "N", "0|1|2"),
                    ],
                },
            ]
        },
        9: {
            "__flags": [
                "key-value",
                {
                    "non-mandatory values": [
                        ("NOT_WIM_LANE", "str"),
                        ("ON_SCALE_MISSED", "str"),
                        ("SPEED_CHANGE", "str"),
                        ("WEIGHT_DIFF", "str"),
                        ("PARTIAL_AXLE", "str"),
                        ("UNEQUAL_AXLE", "str"),
                        ("WRONG_LANE", "str"),
                        ("DRIVER_ISSUE", "str"),
                        ("HARDWARE_ISSUE", "str"),
                        ("INVALID_MEASUREMENT", "str"),
                    ],
                },
            ]
        },
        10: {
            "vehicle": {
                "plate": [
                    {
                        "country": "ISO3166_1_int",
                        "text": "str",
                        "placement": "front|rear",
                        "precision": "int_0_100",
                    }
                ],
                "params": [
                    "key-value",
                    {"values": [("class", "vehicle_class"), ("lane", "+int_0")]},
                ],
                "axlesLayout": "numeric_array",
            }
        },
        11: {
            "media": [
                {
                    "type": "media_type",
                    "baseurl": "str",
                    "name": "str",
                    "hash": "hash_array",
                    "datetime": "ISO8601",
                }
            ]
        },
    }

    VEHICLE_TYPES = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    VEHICLE_TYPE_SCHEMA = {
        3: [[[1], [2]]],
        4: [[[1], [2]]],
        5: [[1], [2, 3]],
        6: [[[1], [2], [3, 4]], [[1, 2], [3, 4]]],
        7: [[[1], [2], [3, 4, 5]]],
        8: [[[1], [2], [3], [4]]],
        9: [[[1], [2, 3], [4], [5]], [[1], [2, 3], [4, 5]]],
        10: [[[1], [2], [3], [4, 5]]],
        11: [[[1], [2, 3], [4], [5, 6]]],
        12: [[[1], [2], [3]]],
        13: [[[1], [2], [3, 4]]],
        14: [[[1], [2], [3, 4, 5]]],
        15: [[[1], [2, 3], [4, 5]]],
        16: [[[1], [2, 3], [4, 5, 6]]],
    }

    @classmethod
    def __validate(cls, json_obj):
        global log

        def is_valid_uuid(uuid_to_test):
            try:
                return str(uuid.UUID(uuid_to_test)) == uuid_to_test
            except ValueError:
                return False

        def is_valid_datetime_ISO8601(dt_to_test):
            regex = r"^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$"
            match_ISO_8601 = re.compile(regex).match
            try:
                return match_ISO_8601(dt_to_test) is not None
            except:
                return False

        def is_valid_WGS84(coord_to_test):
            regex = r"^[0-9]+\.[0-9]+$"
            match_WGS_84 = re.compile(regex).match
            try:
                return match_WGS_84(str(coord_to_test)) is not None
            except:
                return False

        def is_valid_numerical(number_to_test):
            regex = r"^-?[0-9]+$"
            match_number = re.compile(regex).match
            try:
                return match_number(str(number_to_test)) is not None
            except:
                return False

        def is_valid_ISO3166_1(number_to_test):
            if not isinstance(number_to_test, int):
                return False
            number_to_test = str(number_to_test)
            regex = r"^[0-9]{3}$"
            match_number = re.compile(regex).match
            try:
                return match_number(str(number_to_test)) is not None
            except:
                return False

        def is_numeric_array(object_to_test):
            if not isinstance(object_to_test, list):
                return False
            for item in object_to_test:
                if not isinstance(item, list):
                    return False
                for element in item:
                    if not isinstance(element, int) or element <= 0:
                        return False
            return True

        def add_dependent_values(json_schema, json_data):
            if "dependent-values" in json_schema.keys():
                for item in json_schema["dependent-values"]:
                    x_value = item[0]
                    quantity = 0
                    # search for received value
                    for data_element in json_data:
                        if isinstance(data_element, dict) and all(
                            item in data_element.keys() for item in ("key", "value")
                        ):
                            key, value = data_element["key"], int(data_element["value"])
                            if key == x_value and type_validators["+int"](str(value)):
                                quantity = value + item[1]
                                break
                    if quantity:
                        for i in range(1, quantity + 1):
                            key = item[2].replace(item[3], str(i))
                            value = item[4]
                            json_schema["values"].append((key, value))
        
        def check_for_keys(keys_type, json_schema, json_data, data_copy, path):
            result = True
            if keys_type in json_schema.keys():
                for data_element in json_data:
                    if isinstance(data_element, dict) and all(
                        item in data_element.keys() for item in ("key", "value")
                    ):
                        key, value = data_element["key"], str(data_element["value"])
                        # search for key in schema
                        for item in json_schema[keys_type]:
                            if key == item[0]:
                                if not type_validators[item[1]](value):
                                    result = False
                                    log[path + f"key:{key}:"] = f"value type mismatch: {value} is not of type: {item[1]}"
                                json_schema[keys_type].remove(item)
                                data_copy.remove(data_element)
                                break
            return result

        def validate_key_value_array(json_schema, json_data, path):
            result = True

            # adding dependent items to schema
            meta = copy.deepcopy(json_schema)
            add_dependent_values(meta, json_data)

            # checking mandatory keys
            data = copy.deepcopy(json_data)
            result = check_for_keys("values", meta, json_data, data, path) and result

            # checking non-mandatory keys
            result = check_for_keys("non-mandatory values", meta, copy.deepcopy(data), data, path) and result

            # check if there are left some unreceived key-value objects
            if "values" in meta.keys():
                for item in meta["values"]:
                    result = False
                    log[path + f"key:{item[0]}:"] = "missing value"

            return result

        def validate_element_structural(json_schema, json_data, path):
            result = True

            for key_ in json_schema.keys():
                # check that particular key is mandatory or not
                key = key_[2:] if key_.startswith("__") else key_
    
                # check that particular key is present in given json data (only for mandatory keys)
                if key not in json_data.keys():
                    if not key_.startswith("__"):
                        result = False
                        log[path + key] = "missing value"
                    continue

                value = json_schema[key_]
                # if value is a single string
                if isinstance(value, str):
                    # check type for data type according to json_schema
                    if not type_validators[value](json_data[key]):
                        result = False
                        log[path + key] = f"type mismatch: {json_data[key]} is not of type: {value}"
                # value is a container
                else:
                    # check for type compatibility
                    if not isinstance(value, type(json_data[key])):
                        result = False
                        log[path + key] = f"type mismatch: {json_data[key]} is not of type: {type(value)}"
                    # if value is a dictionary
                    elif isinstance(value, dict) :
                        result = result and validate_element_structural(value, json_data[key], path +key + ".")
                    # if value is a list
                    elif isinstance(value, list):
                        # check if it is key-value array
                        if value[0] == "key-value":
                            result = validate_key_value_array(value[1], json_data[key], path + key + ".")
                        # or it is ordinar array: just iterate through it
                        else:
                            for data in json_data[key]:
                                result = validate_element_structural(value[0], data, path + key + ".")

            return result

        # TODO: add functional compliance testing
        def validate_element_functional(json_data):
            return True


        result = True
        log = dict()

        type_validators = {
            "UUID": is_valid_uuid,
            "str": lambda x: True,
            "ISO8601": is_valid_datetime_ISO8601,
            "WGS84": is_valid_WGS84,
            "+int": lambda x: x.isdigit() and int(x) > 0,
            "+int_0": lambda x: x.isdigit(),
            "int_0_100": lambda x: isinstance(x, int) and 0 <= x <= 100,
            "int": is_valid_numerical,
            "0|1|2": lambda x: str(x) == "0" or str(x) == "1" or str(x) == "2",
            "ISO3166_1_int": is_valid_ISO3166_1,
            "front|rear": lambda x: x == "front" or x == "rear",
            "vehicle_class": lambda x: ((isinstance(x, str) and x.isdigit()) or isinstance(x, int)) and 3 <= int(x) <= 20,
            "numeric_array": is_numeric_array,
            "media_type": lambda x: x in ["plate", "plater", "front", "rear", "side", "sideb"],
            "hash_array": lambda x: isinstance(x, list) and len(x) == 2,
        }

        # do structural checking: compliance with json schema
        for group in cls.JSON_SCHEMA:
            print(f"{group}: {cls.JSON_SCHEMA[group].items()}")
            result = validate_element_structural(cls.JSON_SCHEMA[group], json_obj, "") and result

        # do functional checking    
        result = validate_element_functional(json_obj) and result

        if result:
            return True, None
        else:
            return False, json.dumps(log)


    @classmethod
    def validate_json_file(cls, json_file):
        """
        Validates JSON file according to the requirements of WAGA API version 1.0.5.

        Parameters:
        -----------
        json_file: str
            Path to the JSON file to validate

        Output:
        -----------
        (True, None) or (False, {json_str_with_details})
        """
        try:
            with open(json_file, "r", encoding="utf-8") as reader:
                json_obj = json.load(reader)
        except FileNotFoundError:
            return False, {"message": "Can't load given json file: file not found"}
        except json.decoder.JSONDecodeError:
            return False, {
                "message": "Can't load given json file: file is in invalid JSON format"
            }
        except Exception:
            return False, {"message": "Can't load given json file"}

        return cls.__validate(json_obj)

    @classmethod
    def validate_json_str(cls, json_str):
        """
        Validates json in string format according to the requirements of WAGA API version 1.0.5.

        Parameters:
        -----------
        json_str: str
            JSON in string format

        Output:
        -----------
        (True, None) or (False, {json_str_with_details})
        """
        try:
            json_obj = json.loads(json_str)
        except json.decoder.JSONDecodeError:
            return False, {
                "message": "Can't decode given string: string is in invalid JSON format"
            }
        except Exception:
            return False, {"message": "Can't decode given string"}

        return cls.__validate(json_obj)


if __name__ == "__main__":
    print("Start in debug mode")
    # print('Validating file:', sys.argv[1])
    # WAGA_JSON_VALIDATOR_1_0_5.validate_json_file(sys.argv[1])

    result = WAGA_JSON_VALIDATOR_1_0_5.validate_json_file("Pass_8633.json")
    # result = WAGA_JSON_VALIDATOR_1_0_5.validate_json_file("2.json")
    if result[0]:
        print("OK")
    else:
        print("not OK")
        print(json.loads(result[1]))
        json.dump(json.loads(result[1]), open("result.json", "w", encoding="utf-8"))
