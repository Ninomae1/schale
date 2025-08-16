import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ブルアカ育成アプリ')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              child: const Text('キャラクター一覧'),
              onPressed: () => Navigator.pushNamed(context, '/characters'),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              child: const Text('素材一覧'),
              onPressed: () => Navigator.pushNamed(context, '/items'),
            ),
          ],
        ),
      ),
    );
  }
}