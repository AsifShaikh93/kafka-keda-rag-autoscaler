from locust import HttpUser, task, between

class RAGUser(HttpUser):

    wait_time = between(1,3)

    @task
    def ask(self):

        self.client.post("/query",json={
            "user_input":"Explain quantum computing in simple terms",
            "session_id":"test-user"
        })