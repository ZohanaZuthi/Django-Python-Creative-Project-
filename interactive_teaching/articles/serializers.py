from rest_framework import serializers
from .models import Highlight

class HighlightSerializer(serializers.ModelSerializer):
    image_url=serializers.SerializerMethodField()
    audio_url=serializers.SerializerMethodField()
    video_url=serializers.SerializerMethodField()
    class Meta:
        model = Highlight
        fields = ['id', 'text', 'text_content', 'image_url', 'audio_url', 'video_url', 'url_link', 'external_link']
    
        def get_photo_url(self, obj):
            request=self.context.get('request')
            return request.build_absolute_uri(obj.image.url) if obj.image else None
        def get_audio_url(self, obj):
            request=self.context.get('request')
            return request.build_absolute_uri(obj.audio.url) if obj.audio else None

        def get_video_url(self, obj):
            request=self.context.get('request')
            return request.build_absolute_uri(obj.video.url) if obj.video else None 
            