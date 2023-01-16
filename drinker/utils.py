from hashids import Hashids

def get_hashid(self, Type, *args, **kwargs):
        super(Type,self).save(*args, **kwargs)
        self.slug = Hashids('*N4q8f_/9bTi', min_length=5).encode(self.pk)
        super(Type,self).save()

def generate_hashid(pk):
        id = Hashids('*N4q8f_/9bTi', min_length=5).encode(pk)
        return id