class MaterialInfo {
  final int level;
  final Map<String, int> materials; // 素材名と必要数

  MaterialInfo(this.level, this.materials);

  String get materialsText => materials.entries.map((e) => '${e.key} ×${e.value}').join(', ');
}