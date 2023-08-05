def get_environment_variables(config):
    env_keys = list(filter(lambda variable: variable.startswith('ENV_'), config.keys()))
    return list(map(lambda key: {'name': key.replace('ENV_',''), 'value': config[key]}, env_keys))

def get_secret_variables(config):
    env_keys = list(filter(lambda variable: variable.startswith('SECRET_'), config.keys()))
    return list(map(lambda key: {'name': key.replace('SECRET_',''), 'valueFrom': config[key]}, env_keys))

def get_task_definition(config,use_fargate):

    task =  {
        "portMappings": [],
        "image": config['TASK_IMAGE'],
        "essential": True,
        "name": config['TASK_NAME'],
        "environment": get_environment_variables(config),
        "secrets": get_secret_variables(config),
        "entryPoint": eval(config['ENTRYPOINT']),
        "command": eval(config['COMMAND']),
        "links": []
    }

    if "TASK_MEMORY_RESERVATION" in config:
        task["memoryReservation"] = int(config['TASK_MEMORY_RESERVATION'])

    if "PORT_MAPPING_CONTAINER_PORT" in config:
        task["portMappings"].append({
            "containerPort": int(config['PORT_MAPPING_CONTAINER_PORT']),
            "hostPort": int(config['PORT_MAPPING_HOST_PORT']),
            "protocol": config['PORT_MAPPING_PROTOCOL'],
        })

    if not use_fargate:
        task["cpu"] = int(config['TASK_CPU'])
        task["memory"] = int(config['TASK_MEMORY'])

    if "FLUENTD_HOST" in config:
        task["logConfiguration"] = {
            "logDriver": "fluentd",
            "options": {
                "fluentd-address": config['FLUENTD_HOST'],
                "tag": "logs.{}.{}".format(config['FAMILY'],config['ENV'])
            }
        }
    else:
        task["logConfiguration"] = {
            "logDriver": "awslogs",
            "options": {
                'awslogs-group': config['FAMILY'],
                'awslogs-region': config['REGION']
            }
        }
        if use_fargate:
            task["logConfiguration"]["options"]["awslogs-stream-prefix"] = "aws-fargate/"

    return [task]



