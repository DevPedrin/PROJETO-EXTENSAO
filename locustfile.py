import random
import re

from locust import HttpUser, task, between

USER_CREDENTIALS = [
    ("admin", "ifto2026"),
    ("moderador", "ifto2026"),
    ("usuario", "ifto2026"),
]

CSRF_TOKEN_RE = re.compile(r'name=["\']csrfmiddlewaretoken["\']\s+value=["\']([^"\']+)["\']')


def extract_csrf_token(text: str) -> str | None:
    match = CSRF_TOKEN_RE.search(text)
    return match.group(1) if match else None


class PortalUser(HttpUser):
    wait_time = between(1, 4)

    def on_start(self) -> None:
        self.login()

    def login(self) -> None:
        response = self.client.get("/accounts/login/", name="Login page")
        csrf_token = extract_csrf_token(response.text)
        if not csrf_token:
            return

        username, password = random.choice(USER_CREDENTIALS)
        self.client.post(
            "/accounts/login/",
            data={
                "username": username,
                "password": password,
                "csrfmiddlewaretoken": csrf_token,
            },
            headers={"Referer": f"{self.host}/accounts/login/"},
            name="Login",
        )

    @task(3)
    def home(self) -> None:
        self.client.get("/", name="Home")

    @task(2)
    def videos(self) -> None:
        self.client.get("/videos/", name="Videos")

    @task(2)
    def delegacias(self) -> None:
        self.client.get("/delegacias/", name="Delegacias")

    @task(1)
    def estatisticas(self) -> None:
        self.client.get("/estatisticas/", name="Estatisticas")

    @task(2)
    def denuncias_publicadas(self) -> None:
        self.client.get("/denuncias-publicadas/", name="Denuncias Publicadas")

    @task(1)
    def documentacao(self) -> None:
        self.client.get("/documentacao/", name="Documentacao")

    @task(2)
    def dashboard(self) -> None:
        self.client.get("/dashboard/", name="Dashboard")

    @task(1)
    def profile(self) -> None:
        self.client.get("/accounts/profile/", name="Profile")

    @task(1)
    def logout_and_relogin(self) -> None:
        self.client.get("/accounts/logout/", name="Logout")
        self.login()
