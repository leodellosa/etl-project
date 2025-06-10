def user_details_processor(request):
    user_details = request.session.get('user_details')
    # print(f"User details in context processor: {user_details}")  # Debugging line
    return {'user_details': user_details}
