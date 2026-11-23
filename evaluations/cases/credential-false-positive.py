TEST_PLACEHOLDER = "REPLACE_WITH_TEST_TOKEN"

def configure(headers, supplied_token):
    headers["Authorization"] = "Bearer " + supplied_token
