def test_home_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_template_used(client):
    response = client.get('/')
    templates = response.templates
    assert 'core/core.html' in [template.name for template in templates]


