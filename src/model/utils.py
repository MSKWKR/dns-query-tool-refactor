import pickle


def dictionary_value_to_bytes(search_results: dict) -> dict:
    """
    Helper function for taking the searched result and pickle all field values except for search_used_time and check_time
    :param search_results: The DNS search result
    :type: dict

    :return: The altered dictionary
    :rtype: dict
    """
    for record_key in search_results:
        if record_key in ["search_used_time", "check_time"]:
            continue

        search_results[record_key] = pickle.dumps(search_results[record_key])

    return search_results
