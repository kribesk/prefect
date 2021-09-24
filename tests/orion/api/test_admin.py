import prefect


async def test_hello_world(client):
    response = await client.get("/admin/hello")
    assert response.status_code == 200
    assert response.json() == "👋"


class TestSettings:
    async def test_read_settings(self, client):
        response = await client.get("/admin/settings")
        assert response.status_code == 200
        parsed_settings = prefect.utilities.settings.Settings.parse_obj(
            response.json()
        ).dict()
        prefect_settings = prefect.settings.copy().dict()

        # remove secret strings because they break equality
        del parsed_settings["orion"]["database"]["connection_url"]
        del prefect_settings["orion"]["database"]["connection_url"]

        assert parsed_settings == prefect_settings


async def test_version(client):
    response = await client.get("/admin/version")
    assert response.status_code == 200
    assert prefect.__version__
    assert response.json() == prefect.__version__
