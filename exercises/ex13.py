import requests
import pytest

user_agents = [
    ({
        "User agent": "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30"
                      " (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        "Expected values": {
            "platform": "Mobile",
            "browser": "No",
            "device": "Android"
        }
    }),
    ({
        "User agent": "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
                      " CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        "Expected values": {
            "platform": "Mobile",
            "browser": "Chrome",
            "device": "iOS"
        }
    }),
    ({
        "User agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Expected values": {
            "platform": "Googlebot",
            "browser": "Unknown",
            "device": "Unknown"
        }
    }),
    ({
        "User agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        "Expected values": {
            "platform": "Web",
            "browser": "Chrome",
            "device": "No"
        }
    }),
    ({
        "User agent": "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)"
                      " Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Expected values": {
            "platform": "Mobile",
            "browser": "No",
            "device": "iPhone"
        }
    })
]


class TestUserAgent:
    @pytest.mark.parametrize("user_agent", user_agents)
    def test_check_user_agent(self, user_agent):
        url = 'https://playground.learnqa.ru/ajax/api/user_agent_check'
        headers = {
            "User-Agent": user_agent['User agent']
        }
        response = requests.get(url, headers=headers).json()
        assert user_agent['Expected values']['platform'] == response['platform'], \
            f'For "{user_agent["User agent"]}" expected value in not equal to actual.Actual is - {response["platform"]}'
        assert user_agent['Expected values']['browser'] == response['browser'], \
            f'For "{user_agent["User agent"]}" expected value in not equal to actual. Actual is - {response["browser"]}'
        assert user_agent['Expected values']['device'] == response['device'], \
            f'For "{user_agent["User agent"]}" expected value in not equal to actual. Actual is - {response["device"]}'
