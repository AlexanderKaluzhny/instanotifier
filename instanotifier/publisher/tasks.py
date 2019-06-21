from celery import shared_task

from instanotifier.publisher.email.publisher import RssNotificationEmailPublisher


@shared_task
def publish(saved_pks, feedsource_pk):
    publisher = RssNotificationEmailPublisher(saved_pks, feedsource_pk)
    publisher.publish()
