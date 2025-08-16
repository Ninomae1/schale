import 'package:flutter/material.dart';
import '../models/material_info.dart';

class SkillLevelRow extends StatelessWidget {
  final String skillName;
  final int currentLevel;
  final int targetLevel;
  final List<MaterialInfo> materials;

  const SkillLevelRow({
    super.key,
    required this.skillName,
    required this.currentLevel,
    required this.targetLevel,
    required this.materials,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(skillName, style: const TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(width: 8),
        Text('Lv.$currentLevel → Lv.$targetLevel'),
        IconButton(
          icon: const Icon(Icons.info_outline),
          onPressed: () {
            showDialog(
              context: context,
              builder: (_) => AlertDialog(
                title: Text('$skillName 必要素材'),
                content: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: materials
                    .where((m) => m.level > currentLevel && m.level <= targetLevel)
                    .map((m) => ListTile(
                      title: Text('Lv.${m.level}'),
                      subtitle: Text(m.materialsText),
                    ))
                    .toList(),
                ),
                actions: [
                  TextButton(child: const Text('閉じる'), onPressed: () => Navigator.pop(context)),
                ],
              ),
            );
          },
        ),
      ],
    );
  }
}