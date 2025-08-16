class Item {
  final String id;
  final String name;
  final String iconFile;
  final String description;
  final int requiredCount;

  Item({
    required this.id,
    required this.name,
    required this.iconFile,
    required this.description,
    required this.requiredCount,
  });

  factory Item.fromCsv(List<dynamic> row) {
    return Item(
      id: row[0].toString(),
      name: row[1].toString(),
      iconFile: row[2].toString(),
      description: row[3].toString(),
      requiredCount: int.tryParse(row[4].toString()) ?? 0,
    );
  }
}