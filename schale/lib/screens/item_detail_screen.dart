import 'package:flutter/material.dart';
import '../models/item.dart';

class ItemDetailScreen extends StatelessWidget {
  final Item item;
  const ItemDetailScreen({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(item.name)),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Image.asset('assets/items/item_icons/${item.iconFile}', width: 80, height: 80),
            const SizedBox(height: 16),
            Text(item.description, style: const TextStyle(fontSize: 16)),
            const SizedBox(height: 32),
            Text('必要数: ${item.requiredCount}', style: const TextStyle(fontSize: 18)),
            // ここにどのキャラ・どのスキルで使うかなど詳細情報を表示も可能
          ],
        ),
      ),
    );
  }
}