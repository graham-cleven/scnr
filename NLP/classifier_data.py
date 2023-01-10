#!/usr/bin/env python3


def get_traning_data():
    training_data = []
    training_data.append({"class": "processes", "sentence": "show processes"})
    training_data.append({"class": "processes", "sentence": "show all processes"})
    training_data.append({"class": "processes", "sentence": "show processes on"})
    training_data.append({"class": "processes", "sentence": "show all processes on"})
    training_data.append({"class": "processes", "sentence": "show running processes"})
    training_data.append(
        {"class": "processes", "sentence": "show all running processes on"}
    )
    training_data.append(
        {"class": "processes", "sentence": "show all running processes"}
    )

    training_data.append({"class": "specific_process", "sentence": "show process"})
    training_data.append({"class": "specific_process", "sentence": "process"})

    training_data.append({"class": "services", "sentence": ""})
    training_data.append({"class": "running_services", "sentence": ""})
    training_data.append({"class": "applications", "sentence": ""})
    training_data.append({"class": "ports", "sentence": ""})
    training_data.append({"class": "logged_in_users", "sentence": ""})
    training_data.append({"class": "existing_users", "sentence": ""})
    return training_data
