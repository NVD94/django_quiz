from rest_framework import serializers

from quizzes.models import Quiz, Question, Answer
from . import QuestionSerializerInput, UserSerializerOutput, QuestionSerializerOutput


from django.contrib.auth.models import User


class QuizSerializerInput(serializers.ModelSerializer):
    questions = QuestionSerializerInput(many=True)

    class Meta:
        model = Quiz
        fields = ["user", "name", "summary", "questions"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions")
        user = validated_data.pop("user")
        if user is None:
            raise serializers.ValidationError({"detail": "user does not exist"})
        print("cenas")
        quiz = Quiz.objects.create(user=user, **validated_data)
        for question_data in questions_data:
            answers_data = question_data.pop("answers")
            question = Question.objects.create(quiz=quiz, **question_data)
            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)
        return quiz

    def update(self, instance, validated_data):
        request_orders_data = validated_data.pop("request_orders")
        orders = instance.request_orders.all()
        orders = list(orders)
        instance.origin = validated_data.get("origin", instance.origin)
        instance.save()

        for request_order_data in request_orders_data:
            request_order_items_data = request_order_data.pop("request_order_itemss")
            items = instance.request_orders.get().request_order_itemss.all()
            items = list(items)
            for request_order_item_data in request_order_items_data:
                item = items.pop(0)
                item.product_id = request_order_item_data.get(
                    "product_id", item.product_id
                )
                item.qty = request_order_item_data.get("qty", item.qty)
                item.save()
            order = orders.pop(0)
            order.position = request_order_data.get("position", order.position)
            order.destination = request_order_data.get("destination", order.destination)
            order.order_ref = request_order_data.get("order_ref", order.order_ref)
            order.save()
        return instance


class QuizSerializerOutput(serializers.ModelSerializer):
    questions = QuestionSerializerOutput(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "name", "summary", "questions"]


class QuizSimpleSerializerOutput(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ["id", "name", "summary"]
