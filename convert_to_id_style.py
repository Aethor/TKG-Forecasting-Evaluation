# This script converts a temporal knowledge graph forecasting dataset
# of this form:
#
# entity2id.json
# relation2id.json
# ts2id.json
# test.txt  <
# train.txt < each line in these files of the form SUBJECT \t RELATION \t OBJECT \t TIMESTAMP
# valid.txt <
#
# to a dataset of this form:
#
# entity2id.txt   < each line in this file of the form ENTITY \t ID
# relation2id.txt < each line in this file of the form RELATION \t ID
# test.txt  <
# train.txt < each line in these files of the form SUBJ_ID \t REL_ID \t OBJ_ID \t TS_ID
# valid.txt <
import json, os, shutil
import pathlib as pl


def convert_facts_to_id_style(
    in_path: pl.Path,
    out_path: pl.Path,
    ent2id: dict[str, str],
    rel2id: dict[str, str],
    ts2id: dict[str, str],
):
    facts = []
    with open(in_path) as f:
        for line in f:
            subj, rel, obj, ts = line.rstrip("\n").split("\t")
            facts.append((subj, rel, obj, ts))

    with open(out_path, "w") as f:
        for subj, rel, obj, ts in facts:
            f.write(
                "{}\t{}\t{}\t{}\n".format(
                    ent2id[subj], rel2id[rel], ent2id[obj], ts2id[ts]
                )
            )


def convert_iddict_to_id_style(iddict: dict[str, str], out_path: pl.Path):
    with open(out_path, "w") as f:
        for key, key_id in iddict.items():
            f.write(f"{key}\t{key_id}\n")


def convert_dataset_to_id_style(in_dir: pl.Path, out_dir: pl.Path):
    os.makedirs(out_dir, exist_ok=True)

    with open(in_dir / "entity2id.json") as f:
        ent2id = json.load(f)
    with open(in_dir / "relation2id.json") as f:
        rel2id = json.load(f)
    with open(in_dir / "ts2id.json") as f:
        ts2id = json.load(f)

    convert_facts_to_id_style(
        in_dir / "train.txt", out_dir / "train.txt", ent2id, rel2id, ts2id
    )
    convert_facts_to_id_style(
        in_dir / "valid.txt", out_dir / "valid.txt", ent2id, rel2id, ts2id
    )
    convert_facts_to_id_style(
        in_dir / "test.txt", out_dir / "test.txt", ent2id, rel2id, ts2id
    )

    convert_iddict_to_id_style(ent2id, out_dir / "entity2id.txt")
    convert_iddict_to_id_style(rel2id, out_dir / "relation2id.txt")
    convert_iddict_to_id_style(ts2id, out_dir / "ts2id.txt")

    shutil.copy(in_dir / "stat.txt", out_dir / "stat.txt")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-dir", type=pl.Path)
    parser.add_argument("-o", "--output-dir", type=pl.Path)
    args = parser.parse_args()

    convert_dataset_to_id_style(args.input_dir, args.output_dir)
