class Skill {
  final String type; // EX, ノーマル, パッシブ, サブ, etc
  final int level;
  final Map<String, int> materials;

  Skill({required this.type, required this.level, required this.materials});

  factory Skill.fromCsvRow(List<dynamic> row) {
    String type = row[0].toString();
    int level = int.tryParse(row[1].toString()) ?? 0;
    Map<String, int> materials = {};
    for (int i = 2; i < row.length; i += 2) {
      if (row[i] != null && row[i].toString().isNotEmpty) {
        materials[row[i].toString()] = int.tryParse(row[i + 1].toString()) ?? 0;
      }
    }
    return Skill(type: type, level: level, materials: materials);
  }
}