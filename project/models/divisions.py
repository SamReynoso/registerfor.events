from models.models import Division

    # TODO:
    # On delete notify of canceled registrations.


class DivisionCRUD:

    @staticmethod
    def create(*args, **kwargs):
        ret = Division.objects.create(*args, **kwargs)
        return ret

    @staticmethod
    def delete(division: Division):
        ret =  division.delete()
        # Notify of all the cancellations.
        return ret
