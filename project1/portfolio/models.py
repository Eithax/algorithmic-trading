from django.db import models

class Portfolio(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    initial_cash = models.DecimalField(max_digits=15, decimal_places=2)
    current_cash = models.DecimalField(max_digits=15, decimal_places=2)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    snaptrade_user_id = models.CharField(max_length=100, blank=True)
    snaptrade_account_id = models.CharField(max_length=100, blank=True)
    snaptrade_user_secret = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portfolios"
        ordering = ["name"]

class Position(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="positions")
    stock = models.ForeignKey("trading.Stock", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    average_cost = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    curent_price = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    current_value = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    unrealized_pnl = models.DecimalField(max_digits=15, decimal_places=4, default=0)
    unrealized_pnl_percent = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "positions"
        unique_together = ("portfolio", "stock")
        ordering = ["-current_value"]

class Trade(models.Model):
    TRADE_TYPES = [
        ("BUY", "Buy"),
        ("SELL", "Sell"),
    ]

    STATUS_CHOICES = [
            ("PENDING", "Pending"),
            ("SUBMITTED", "Submitted"),
            ("FILLED", "Filled"),
            ("PARTIALLY_FILLED", "Partially Filled"),
            ("CANCELLED", "Cancelled"),
            ("REJECTED", "Rejected"),
        ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="trades")
    stock = models.ForeignKey("trading.Stock", on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    filled_quantity = models.IntegerField(default=0)
    filled_price = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    order_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    external_order_id = models.CharField(max_length=100, blank=True)
    snaptrade_order_id = models.CharField(max_length=100, blank=True)
    comission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    error_message = models.TextField(blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    filled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "trades"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["portfolio", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]

class PerformanceMetrics(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="porformance_metrics")
    date = models.DateField()
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    cash_value = models.DecimalField(max_digits=15, decimal_places=2)
    positions_value = models.DecimalField(max_digits=15, decimal_places=2)
    daily_return = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    cumulative_return = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    total_trades = models.IntegerField(default=0)
    winning_trades = models.IntegerField(default=0)
    losing_trades = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "performance_metrics"
        unique_together = ("portfolio", "date")
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["portfolio", "date"]),
        ]