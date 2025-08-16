import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:csv/csv.dart';
import '../models/character.dart';
import '../models/skill.dart';
import '../models/material_info.dart';
import '../widgets/skill_level_row.dart';

class CharacterDetailScreen extends StatefulWidget {
  final Character character;
  const CharacterDetailScreen({super.key, required this.character});

  @override
  State<CharacterDetailScreen> createState() => _CharacterDetailScreenState();
}

class _CharacterDetailScreenState extends State<CharacterDetailScreen> {
  Map<String, int> currentLevels = {};
  Map<String, int> targetLevels = {};
  Map<String, List<MaterialInfo>> skillMaterials = {};

  @override
  void initState() {
    super.initState();
    loadSkills();
    // 初期値は仮でLv1→Lv5
    for (var skillName in ['EXスキル', 'ノーマルスキル', 'パッシブスキル', 'サブスキル', '限界突破', '固有武器', '能力開放_最大HP', '能力開放_攻撃力', '能力開放_治癒力']) {
      currentLevels[skillName] = 1;
      targetLevels[skillName] = 5;
    }
  }

  Future<void> loadSkills() async {
    final skillFile = 'assets/characters/skill/${widget.character.name}.csv';
    try {
      final csvString = await rootBundle.loadString(skillFile);
      final csvRows = const CsvToListConverter().convert(csvString, eol: '\n');
      Map<String, List<MaterialInfo>> matMap = {};
      for (var row in csvRows) {
        if (row.length < 3) continue;
        String type = row[0].toString();
        int level = int.tryParse(row[1].toString()) ?? 1;
        Map<String, int> mats = {};
        for (int i = 2; i < row.length; i += 2) {
          if (row[i] != null && row[i].toString().isNotEmpty) {
            mats[row[i].toString()] = int.tryParse(row[i + 1].toString()) ?? 0;
          }
        }
        matMap[type] = (matMap[type] ?? [])..add(MaterialInfo(level, mats));
      }
      setState(() { skillMaterials = matMap; });
    } catch (e) {
      // ファイルがない場合もあるので無視
    }
  }

  Widget buildLevelRow(String skillName) {
    final mats = skillMaterials[skillName] ?? [];
    return SkillLevelRow(
      skillName: skillName,
      currentLevel: currentLevels[skillName] ?? 1,
      targetLevel: targetLevels[skillName] ?? 5,
      materials: mats,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.character.name)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Center(
            child: Image.asset(
              'assets/icons/${widget.character.iconFile}',
              width: 100, height: 100,
              errorBuilder: (c, e, s) => const Icon(Icons.image_not_supported),
            ),
          ),
          const SizedBox(height: 16),
          for (var skillName in [
            'EXスキル',
            'ノーマルスキル',
            'パッシブスキル',
            'サブスキル',
            '限界突破',
            '固有武器',
            '能力開放_最大HP',
            '能力開放_攻撃力',
            '能力開放_治癒力',
          ])
          buildLevelRow(skillName),
        ],
      ),
    );
  }
}