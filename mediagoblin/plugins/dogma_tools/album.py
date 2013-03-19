from mediagoblin import messages, mg_globals
from mediagoblin.db.models import (Collection,CollectionItem)
from mediagoblin.tools.response import redirect
from mediagoblin.tools.translate import pass_to_ugettext as _

def album_tools(request, media, collection_form, new_media=False):
    # If we are here, method=POST and the form is valid, submit things.
    # If the user is adding a new collection, use that:
    if request.form['collection_title']:
        # Make sure this user isn't duplicating an existing collection
        existing_collection = Collection.query.filter_by(
                                creator=request.user.id,
                                title=request.form['collection_title']).first()
        if existing_collection:
            messages.add_message(request, messages.ERROR,
                _('You already have a collection called "%s"!')
                % existing_collection.title)
            return redirect(request, "mediagoblin.user_pages.media_home",
                            user=media.get_uploader.username,
                            media=media.slug_or_id)

        collection = Collection()
        collection.title = request.form['collection_title']
        collection.description = request.form.get('collection_description')
        collection.creator = request.user.id
        collection.generate_slug()
        collection.save()

    # Otherwise, use the collection selected from the drop-down
    else:
        collection = Collection.query.filter_by(
            id=request.form.get('collection'),
            creator=request.user.id).first()

    # Make sure the user actually selected a collection
    if not collection:
        messages.add_message(
            request, messages.ERROR,
            _('You have to select or add a collection'))
        return redirect(request, "mediagoblin.user_pages.media_collect",
                    user=media.get_uploader.username,
                    media_id=media.id)


    # Check whether media already exists in collection
    elif CollectionItem.query.filter_by(
        media_entry=media.id,
        collection=collection.id).first():
        messages.add_message(request, messages.ERROR,
                             _('"%s" already in collection "%s"')
                             % (media.title, collection.title))
    else: # Add item to collection
        collection_item = request.db.CollectionItem()
        collection_item.collection = collection.id
        collection_item.media_entry = media.id
        collection_item.note = request.form['note']
        collection_item.save()

        collection.items = collection.items + 1
        collection.save()

        media.collected = media.collected + 1
        media.save()

        messages.add_message(request, messages.SUCCESS,
                             _('"%s" added to collection "%s"')
                             % (media.title, collection.title))

    return redirect(request, "mediagoblin.user_pages.media_home",
                    user=media.get_uploader.username,
                    media=media.slug_or_id)
