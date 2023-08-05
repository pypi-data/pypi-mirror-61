from ..helpers import format_result


def get_tools(client, project_id: str):
    result = client.execute('''
    query {
      getTools(projectID: "%s") {
        id
        toolType
        jsonSettings
      }
    }
    ''' % (project_id))
    return format_result('getTools', result)
