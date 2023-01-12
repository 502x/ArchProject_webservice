# recommendations/recommendations.py

from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
	BookCategory,
	BookRecommendation,
	RecommendationResponse,
)

import recommendations_pb2_grpc

books_by_category = {
	BookCategory.MYSTERY: [
		BookRecommendation(id=1, title="Мальтийский сокол"),
		BookRecommendation(id=2, title="Убийство в Восточном экспрессе"),
		BookRecommendation(id=3, title="Собака Баскервилей"),
		BookRecommendation(id=4, title="Автостопом по галактике"),
		BookRecommendation(id=5, title="Иное"),
		BookRecommendation(id=6, title="Астрал"),
		BookRecommendation(id=7, title="Пила"),
		BookRecommendation(id=8, title="Семейка Адамс"),
		BookRecommendation(id=9, title="Шерлок Холмс"),
		BookRecommendation(id=10, title="Человек-бензопила"),
	],

	BookCategory.SCIENCE_FICTION: [
		BookRecommendation(id=11, title="Дюна"),
		BookRecommendation(id=12, title="Интерстеллар"),
		BookRecommendation(id=13, title="Стар-трек"),
		BookRecommendation(id=14, title="Звездные войны"),
		BookRecommendation(id=15, title="Девушка из космоса"),
		BookRecommendation(id=16, title="Астероид"),
		BookRecommendation(id=17, title="Марисианин"),
		BookRecommendation(id=18, title="Андромеда"),
		BookRecommendation(id=19, title="Чужой"),
		BookRecommendation(id=20, title="Ридик"),
	],

	BookCategory.SELF_HELP: [
		BookRecommendation(id=21, title="Семь навыков высокоэффективных людей"),
		BookRecommendation(id=22, title="Как завоёвывать друзей и оказывать влияние на людей"),
		BookRecommendation(id=23, title="Маленький человек - большой человек"),
		BookRecommendation(id=24, title="Лайфхаки для чайников"),
		BookRecommendation(id=25, title="Что такое человек"),
		BookRecommendation(id=26, title="Социум и его структура"),
		BookRecommendation(id=27, title="Познай себя и этот мир"),
		BookRecommendation(id=28, title="Подсказки для выживания на необитаемом острове"),
		BookRecommendation(id=29, title="Хирургическая операция для самых маленьких"),
		BookRecommendation(id=30, title="Что будет если капнуть немного нитроглицерина на порох"),
	],
}
class RecommendationService(recommendations_pb2_grpc.RecommendationsServicer):
	def Recommend(self, request, context):
		if request.category not in books_by_category:
			context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

		books_for_category = books_by_category[request.category]
		num_results = min(request.max_results, len(books_for_category))
		books_to_recommend = random.sample(books_for_category, num_results)

		return RecommendationResponse(recommendations=books_to_recommend)
def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
		RecommendationService(), server
	)
	server.add_insecure_port("[::]:50051")
	server.start()
	server.wait_for_termination()

if __name__ == "__main__":
	serve()