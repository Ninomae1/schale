import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:csv/csv.dart';
import '../models/character.dart';

class CharacterListScreen extends StatefulWidget {
  const CharacterListScreen({super.key});

  @override
  State<CharacterListScreen> createState() => _CharacterListScreenState();
}

class _CharacterListScreenState extends State<CharacterListScreen> {
  List<Character> characters = [];

  @override
  void initState() {
    super.initState();
    loadCharacters();
  }

  Future<void> loadCharacters() async {
    final csvString = await rootBundle.loadString('assets/characters/all_character.csv');
    final csvRows = const CsvToListConverter().convert(csvString, eol: '\n');
    setState(() {
      characters = csvRows.skip(2)
        .where((row) => row.length > 2 && row[2] != null && row[1] != null)
        .map((row) => Character.fromCsv(row)).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('キャラクター一覧')),
      body: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3, childAspectRatio: 0.8,
        ),
        itemCount: characters.length,
        itemBuilder: (context, index) {
          final chara = characters[index];
          return GestureDetector(
            onTap: () {
              Navigator.pushNamed(context, '/character_detail', arguments: chara);
            },
            child: Column(
              children: [
                Image.asset(
                  'assets/icons/${chara.iconFile}',
                  width: 80, height: 80,
                  errorBuilder: (c, e, s) => const Icon(Icons.image_not_supported),
                ),
                Text(
                  chara.name,
                  style: const TextStyle(fontSize: 14),
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}