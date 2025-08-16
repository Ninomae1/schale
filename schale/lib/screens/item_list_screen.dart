import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:csv/csv.dart';
import '../models/item.dart';

class ItemListScreen extends StatefulWidget {
  const ItemListScreen({super.key});

  @override
  State<ItemListScreen> createState() => _ItemListScreenState();
}

class _ItemListScreenState extends State<ItemListScreen> {
  List<Item> items = [];

  @override
  void initState() {
    super.initState();
    loadItems();
  }

  Future<void> loadItems() async {
    final csvString = await rootBundle.loadString('assets/items/all_items.csv');
    final csvRows = const CsvToListConverter().convert(csvString, eol: '\n');
    setState(() {
      items = csvRows.skip(1)
        .where((row) => row.length > 3)
        .map((row) => Item.fromCsv(row)).toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('素材一覧')),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          final item = items[index];
          return ListTile(
            leading: Image.asset('assets/items/item_icons/${item.iconFile}', width: 40, height: 40),
            title: Text(item.name),
            subtitle: Text(item.description),
            trailing: Text('必要数: ${item.requiredCount}'),
            onTap: () => Navigator.pushNamed(context, '/item_detail', arguments: item),
          );
        },
      ),
    );
  }
}