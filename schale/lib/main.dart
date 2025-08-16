import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/character_list_screen.dart';
import 'screens/character_detail_screen.dart';
import 'screens/item_list_screen.dart';
import 'screens/item_detail_screen.dart';
import 'models/character.dart';
import 'models/item.dart';

void main() {
  runApp(const BlueArchiveApp());
}

class BlueArchiveApp extends StatelessWidget {
  const BlueArchiveApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ブルアカ育成アプリ',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/characters': (context) => const CharacterListScreen(),
        '/items': (context) => const ItemListScreen(),
      },
      onGenerateRoute: (settings) {
        if (settings.name == '/character_detail') {
          final Character chara = settings.arguments as Character;
          return MaterialPageRoute(
            builder: (context) => CharacterDetailScreen(character: chara),
          );
        }
        if (settings.name == '/item_detail') {
          final Item item = settings.arguments as Item;
          return MaterialPageRoute(
            builder: (context) => ItemDetailScreen(item: item),
          );
        }
        return null;
      },
    );
  }
}