from app.settings import Settings


def test_get_dotenv_filepath(monkeypatch):
    fake_path = "/fake/path/to/.env"
    monkeypatch.setattr("app.settings._get_dotenv_filepath", lambda: fake_path)

    from app.settings import _get_dotenv_filepath

    assert _get_dotenv_filepath() == fake_path


def test_settings_from_simulated_env(monkeypatch):
    monkeypatch.setenv("DB_URL", "sqlite:///./simulated.db")
    monkeypatch.setenv("JWT_SECRET_KEY", "simulated_secret")
    monkeypatch.setenv("JWT_REFRESH_SECRET_KEY", "simulated_refresh_secret")

    settings = Settings()

    assert settings.db_url == "sqlite:///./simulated.db"
    assert settings.jwt_secret_key == "simulated_secret"
    assert settings.jwt_refresh_secret_key == "simulated_refresh_secret"
