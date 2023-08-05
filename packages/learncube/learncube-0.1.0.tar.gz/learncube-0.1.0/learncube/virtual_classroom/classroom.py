from ..core import LearnCubeBase


class Classroom(LearnCubeBase):

    def __init__(self, public_key, private_key, api_base_path=None):

        super().__init__(public_key, private_key, api_base_path)

    def create_virtual_classroom(self, room_token, **kwargs):
        data = {
            'room_token': room_token
        }
        response = self.post('classrooms/', json={**data, **kwargs})
        if response.status_code != 201:
            raise Exception("Error during creation", response.status_code, response.json())
        else:
            return response.json()

    def list_virtual_classroom(self, **kwargs):
        response = self.get('classrooms/', params=kwargs)
        if response.status_code != 200:
            raise Exception("Error during list", response.status_code, response.json())
        else:
            return response.json()

    def read_virtual_classroom(self, uuid):
        response = self.get('classrooms/{}'.format(uuid))
        if response.status_code != 200:
            raise Exception("Error during read", response.status_code, response.json())
        else:
            return response.json()

    def update_virtual_classroom(self, uuid, **kwargs):
        response = self.put('classrooms/{}/'.format(uuid), json=kwargs)
        if response.status_code != 200:
            raise Exception("Error during update", response.status_code, response.json())
        else:
            return response.json()

    def delete_virtual_classroom(self, uuid):
        response = self.delete('classrooms/{}/'.format(uuid))
        if response.status_code != 204:
            raise Exception("Error during delete", response.status_code, response.json())
        else:
            return response
