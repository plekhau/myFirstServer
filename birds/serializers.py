from rest_framework import serializers

from birds.models import Birds


class BirdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Birds
        fields = ('species', 'name', 'color', 'body_length', 'wingspan')

    # species = serializers.CharField(max_length=255)
    # name = serializers.CharField(max_length=255)
    # color = serializers.CharField(max_length=255)
    # body_length = serializers.IntegerField()
    # wingspan = serializers.IntegerField()
    #
    # def create(self, validated_data):
    #     return Birds.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.species = validated_data.get('species', instance.species)
    #     instance.color = validated_data.get('color', instance.color)
    #     instance.body_length = validated_data.get('body_length', instance.body_length)
    #     instance.wingspan = validated_data.get('wingspan', instance.wingspan)
    #
    #     instance.save()
    #     return instance
