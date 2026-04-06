import traceback
from bson import ObjectId

from db.connection import package_collection
from responses.success import success_status, success_dictionary, no_content
from responses.error import (
    bad_request,
    key_not_exist,
    key_empty,
    data_not_found,
    server_error,
)


def create_package(body):
    try:
        if not body:
            return bad_request("No data provided")

        if "package_name" not in body:
            return key_not_exist("package_name")
        if body["package_name"] == "":
            return key_empty("package_name")

        if "version" not in body:
            return key_not_exist("version")
        if body["version"] == "":
            return key_empty("version")

        if "os" not in body:
            return key_not_exist("os")
        if body["os"] == "":
            return key_empty("os")

        if "environment" not in body or body["environment"] == "":
            return bad_request("Environment (installation path) is required")
        if not isinstance(body["environment"], str):
            return bad_request("Environment must be a valid path string")

        body = dict(body)
        body["namespace"] = "python_env"

        package_collection.insert_one(body)

        return success_status("Package created successfully")

    except Exception as e:
        traceback.print_exc()
        stack = traceback.extract_stack()
        filename, line, procname, text = stack[-1]
        return server_error(procname, str(line), str(e))


def get_all_packages():
    try:
        data = list(package_collection.find())

        if not data:
            return no_content()

        return success_dictionary(data)

    except Exception as e:
        traceback.print_exc()
        stack = traceback.extract_stack()
        filename, line, procname, text = stack[-1]
        return server_error(procname, str(line), str(e))


def get_package(id):
    try:
        data = package_collection.find_one({"_id": ObjectId(id)})

        if not data:
            return data_not_found()

        return success_dictionary(data)

    except Exception as e:
        traceback.print_exc()
        stack = traceback.extract_stack()
        filename, line, procname, text = stack[-1]
        return server_error(procname, str(line), str(e))


def update_package(id, body):
    try:
        if not body:
            return bad_request("No data provided")

        if "environment" in body:
            if body["environment"] == "":
                return key_empty("environment")
            if not isinstance(body["environment"], str):
                return bad_request("Environment must be a valid path string")

        result = package_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": body},
        )

        if result.matched_count == 0:
            return data_not_found()

        return success_status("Package updated successfully")

    except Exception as e:
        traceback.print_exc()
        stack = traceback.extract_stack()
        filename, line, procname, text = stack[-1]
        return server_error(procname, str(line), str(e))


def delete_package(id):
    try:
        result = package_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 0:
            return data_not_found()

        return success_status("Package deleted successfully")

    except Exception as e:
        traceback.print_exc()
        stack = traceback.extract_stack()
        filename, line, procname, text = stack[-1]
        return server_error(procname, str(line), str(e))
