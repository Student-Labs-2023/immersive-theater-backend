from . models import Authors, PerfomanceAuthors, PerfomanceImages, Perfomances, AudioImages, Audio, Places


def get_all_info_about_perfomance(perfomance_id):
    result = dict()
    authors = dict()
    images = list()
    audios = list()
    place = dict()
    perf_query = Perfomances.query.filter_by(id=perfomance_id).first()
    if not perf_query:
        return Exception("Invalid id")
    authors_id_query = PerfomanceAuthors.query.filter_by(perfomance_id=perfomance_id).all()
    for author in authors_id_query:
        authors_query = Authors.query.filter_by(id=author.author_id).first()
        authors.update({'id': authors_query.id, 'full_name': authors_query.full_name, 'image_link': authors_query.thumbnail_link, 'role': author.role})
    audios_query = Audio.query.filter_by(perfomance_id=perfomance_id).all()
    for audio in audios_query:
        audio_images_query = AudioImages.query.filter_by(audio_id=audio.id).all()
        audio_images = list()
        for audio_image in audio_images_query:
            audio_images.append(str(audio_image.image_link))
        places_query = Places.query.filter_by(id=audio.place_id).first()
        place.update({'name': places_query.name, 'latitude': places_query.latitude, 'longitude': places_query.longitude})
        audios.append({'place': place, 'name':audio.name, 'audio_link': audio.audio_link, 'short_audio_link': audio.short_audio_link, 'images': audio_images})

    images_query = PerfomanceImages.query.filter_by(perfomance_id=perfomance_id).all()
    for image in images_query:
        images.append(str(image.image_link))
    result.update({'id': perf_query.id, 'name': perf_query.name, 'image_link': perf_query.thumbnail_link, 'description': perf_query.description, 'duration': perf_query.duration, 'authots': authors, 'images': images, 'audios': audios})
    return result