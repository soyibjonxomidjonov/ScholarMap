# from drf_yasg.utils import swagger_auto_schema
#
#
# @swagger_auto_schema(
#     method='post',
#     request_body=TranslateSerializerConfig, # 2. Mana bu qator Swaggerga "shu maydonlarni ko'rsat" deydi
#     response={201: TranslateSerializerConfig}
# )
# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser]) # Fayllar bilan ishlash uchun shart
# def ai_chat(request):
#     serializer = TranslateSerializerConfig(data=request.data)
#
#     serializer.is_valid(raise_exception=True) # Xatolarni avtomatik qaytaradi
#     text = serializer.validated_data.get('text')
#     file = serializer.validated_data.get('file')
#     response_type = serializer.validated_data.get('response_type', 'text')
#
#     if not text and not file:
#         return JsonResponse({"message": "Matn yoki fayl kiritilishi kerak"}, status=400)
#
#     if file:
#         if response_type == "pdf":
#             response = AI_image_chat(text, file)
#             pdf_response = text_to_pdf(response)
#             http_response = HttpResponse(pdf_response, content_type='application/pdf')
#             http_response['Content-D    isposition'] = 'attachment; filename="chat_response.pdf"'
#             return http_response
#         response = AI_image_chat(text, file)
#         return Response(response)
#     else:
#         if response_type == "pdf":
#             response = AI_chat(text)
#             pdf_response = text_to_pdf(response)
#             http_response = HttpResponse(pdf_response, content_type='application/pdf')
#             http_response['Content-Disposition'] = 'attachment; filename="chat_response.pdf"'
#             return http_response
#         response = AI_chat(text)
#         return Response(response)