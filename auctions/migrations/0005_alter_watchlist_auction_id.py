# Generated by Django 4.2.2 on 2023-08-02 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_watchlist_auction_id_watchlist_auction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auction_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_auction', to='auctions.auctionlist'),
        ),
    ]