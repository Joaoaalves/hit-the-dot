from time import sleep
from . import webpush, WebPushException, json, db, app, Turno,datetime, timedelta

def trigger_push_notification(push_subscription, body):
        try:
                response = webpush(
                        subscription_info=json.loads(push_subscription['subscription_json']),
                        data=json.dumps(body),
                        vapid_private_key=app.config["VAPID_PRIVATE_KEY"],
                        vapid_claims={
                                "sub": "mailto:{}".format(
                                app.config["VAPID_CLAIM_EMAIL"])
                        },
                        ttl=5000
                )
                return response.ok
        except WebPushException as ex:
                if ex.response and ex.response.json():
                        extra = ex.response.json()
                        print("Remote service replied with a {}:{}, {}",
                                extra.code,
                                extra.errno,
                                extra.message
                                )
                return False