from server import Server
import envfileparser

envs = envfileparser.get_env_from_file()

Server.start(
    port=int(envs['SERVER_PORT']),
    address=envs['SERVER_HOST']
)
