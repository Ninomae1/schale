class Character {
  final String name;
  final String iconFile;
  final String rarity;
  final String weaponType;
  final String school;
  // 必要なら他の項目も追加

  Character({
    required this.name,
    required this.iconFile,
    required this.rarity,
    required this.weaponType,
    required this.school,
  });

  // CSVから生成
  factory Character.fromCsv(List<dynamic> row) {
    return Character(
      rarity: row[0].toString(),
      iconFile: row[1].toString(),
      name: row[2].toString(),
      weaponType: row[3].toString(),
      school: row[8].toString(),
    );
  }
}