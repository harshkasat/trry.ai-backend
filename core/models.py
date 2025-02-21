from django.db import models
from authapp.models import User

class URLTable(models.Model):
    url_id = models.AutoField(primary_key=True)
    user_email = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls', default=None)
    url_website = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"<UrlTable(url_id={self.url_id}, url_website={self.url_website})>"
    
    class Meta:
        db_table = 'url_table'

class ExtraURLTable(models.Model):
    url = models.ForeignKey(URLTable, on_delete=models.CASCADE, related_name='extra_urls')
    extra_url_link = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return f"<ExtraURLTable(extra_url_link={self.extra_url_link}, url_id={self.url_id})>"
    
    class Meta:
        db_table = 'extra_url_table'

class StressTable(models.Model):
    extra_url = models.OneToOneField(
        ExtraURLTable,
        on_delete=models.CASCADE,
        primary_key=True,
        to_field='extra_url_link',
        related_name='stress'
    )
    stress_check = models.BooleanField(default=False)

    def __str__(self):
        return f"<StressTable(extra_url_link={self.extra_url_id}, stress_check={self.stress_check})>"
    
    class Meta:
        db_table = 'stress_table'

class PerformanceLighthouseTable(models.Model):
    extra_url = models.OneToOneField(
        ExtraURLTable,
        on_delete=models.CASCADE,
        primary_key=True,
        to_field='extra_url_link',
        related_name='performance'
    )
    performance_lighthouse = models.BooleanField(default=False)

    def __str__(self):
        return f"<PerformanceLighthouseTable(extra_url_link={self.extra_url_id}, performance_lighthouse={self.performance_lighthouse})>"
    
    class Meta:
        db_table = 'performance_lighthouse_table'

class ResponsiveTable(models.Model):
    extra_url = models.OneToOneField(
        ExtraURLTable,
        on_delete=models.CASCADE,
        primary_key=True,
        to_field='extra_url_link',
        related_name='responsive'
    )
    tablet = models.BooleanField(default=False)
    fold_phone = models.BooleanField(default=False)
    normal_phone = models.BooleanField(default=False)
    desktop = models.BooleanField(default=False)

    def __str__(self):
        return f"<ResponsiveTable(extra_url_link={self.extra_url_id}, tablet={self.tablet}, fold_phone={self.fold_phone}, normal_phone={self.normal_phone}, desktop={self.desktop})>"
    
    class Meta:
        db_table = 'responsive_table'  # Fixed: Changed from test_break_table to responsive_table

class TestBreakTable(models.Model):
    extra_url = models.OneToOneField(
        ExtraURLTable,
        on_delete=models.CASCADE,
        primary_key=True,
        to_field='extra_url_link',
        related_name='test_break'
    )
    test_to_break = models.BooleanField(default=False)

    def __str__(self):
        return f"<TestBreakTable(extra_url_link={self.extra_url_id}, test_to_break={self.test_to_break})>"
    
    class Meta:
        db_table = 'test_break_table'