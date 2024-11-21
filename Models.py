from django.db import models


class Area(models.Model):
    area_id = models.IntegerField(primary_key=True)
    area_name = models.CharField(max_length=50)

    def __str__(self):
        return self.area_name


class CrimeLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lon = models.DecimalField(max_digits=10, decimal_places=7)
    cross_street = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.location


class Status(models.Model):
    status_code = models.CharField(max_length=10, primary_key=True)
    status_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.status_desc


class Premise(models.Model):
    premis_cd = models.IntegerField(primary_key=True)
    premis_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.premis_desc


class ReportingDistrict(models.Model):
    rpt_dist_no = models.IntegerField(primary_key=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return f"District {self.rpt_dist_no} ({self.area.area_name})"


class CrimeCode(models.Model):
    crm_cd = models.IntegerField()
    crm_cd_2 = models.IntegerField(default=0)
    crm_cd_3 = models.IntegerField(default=0)
    crm_cd_4 = models.IntegerField(default=0)
    crm_cd_desc = models.CharField(max_length=100)

    class Meta:
        unique_together = (('crm_cd', 'crm_cd_2', 'crm_cd_3', 'crm_cd_4'),)

    def __str__(self):
        return self.crm_cd_desc


class Weapon(models.Model):
    weapon_cd = models.IntegerField(primary_key=True)
    weapon_desc = models.CharField(max_length=100)

    def __str__(self):
        return self.weapon_desc


class CrimeReport(models.Model):
    dr_no = models.IntegerField(primary_key=True)
    date_rptd = models.DateField()
    date_occ = models.DateField()
    time_occ = models.TimeField()
    status_code = models.ForeignKey(Status, on_delete=models.CASCADE)
    premis_cd = models.ForeignKey(Premise, on_delete=models.CASCADE)
    rpt_dist_no = models.ForeignKey(ReportingDistrict, on_delete=models.CASCADE)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    location_id = models.ForeignKey(CrimeLocation, null=True, blank=True, on_delete=models.SET_NULL)
    mocodes = models.CharField(max_length=50, null=True, blank=True)
    weapon_cd = models.ForeignKey(Weapon, null=True, blank=True, on_delete=models.SET_NULL)
    crime_code_crm_cd = models.IntegerField()
    crime_code_crm_cd_2 = models.IntegerField(null=True, blank=True)
    crime_code_crm_cd_3 = models.IntegerField(null=True, blank=True)
    crime_code_crm_cd_4 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Crime Report {self.dr_no}"


class Victim(models.Model):
    vict_id = models.AutoField(primary_key=True)
    dr_no = models.ForeignKey(CrimeReport, on_delete=models.CASCADE)
    vict_age = models.IntegerField()
    vict_sex = models.CharField(max_length=1, null=True, blank=True)
    vict_descent = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return f"Victim {self.vict_id} (Crime Report: {self.dr_no.dr_no})"
