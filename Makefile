TAXONOMY_DIR := raw_data/
PROTEIN = output_data/protein_taxonomy.db
DEAD = output_data/dead_taxonomy.db
NUC = output_data/taxonomy.db

usage:
	@echo -e "Usage:\n'make nucleotide' will create a nucleotide taxonomy db"
	@echo -e "'make dead' will create a dead nucleotide taxonomy db"
	@echo -e "'make protein' will create a protein taxonomy db."
	@echo -e "'make vacuum' will clean up all three DBs."
	@echo -e "'make clean' will remove all three DBs. \n"

all: clean nucleotide dead protein

vacuum:
	./vaccum.sh $(NUC)
	./vaccum.sh $(DEAD)
	./vaccum.sh $(PROTEIN)

# $(DB): clean taxids nodes names hosts

nucleotide:
	echo $(TAXONOMY_DIR) $(NUC)
	rm -f $(NUC)
	./shell/nucleotide-db.sh $(TAXONOMY_DIR)accession2taxid/ $(NUC)
	./shell/add-nodes.sh $(TAXONOMY_DIR)new_taxdump/nodes.dmp $(NUC)
	./shell/add-names.sh $(TAXONOMY_DIR)new_taxdump/names.dmp $(NUC)
	./shell/add-hosts.sh $(TAXONOMY_DIR)new_taxdump/host.dmp $(NUC)

dead:
	echo $(TAXONOMY_DIR) $(DEAD)
	rm -f $(DEAD)
	./shell/dead-db.sh $(TAXONOMY_DIR)accession2taxid/ $(DEAD)
	./shell/add-nodes.sh $(TAXONOMY_DIR)new_taxdump/nodes.dmp $(DEAD)
	./shell/add-names.sh $(TAXONOMY_DIR)new_taxdump/names.dmp $(DEAD)
	./shell/add-hosts.sh $(TAXONOMY_DIR)new_taxdump/host.dmp $(DEAD)

protein:
	echo $(TAXONOMY_DIR) $(PROTEIN)
	rm -f $(PROTEIN)
	./shell/protein-db.sh $(TAXONOMY_DIR)accession2taxid/ $(PROTEIN)
	./shell/add-nodes.sh $(TAXONOMY_DIR)new_taxdump/nodes.dmp $(PROTEIN)
	./shell/add-names.sh $(TAXONOMY_DIR)new_taxdump/names.dmp $(PROTEIN)
	./shell/add-hosts.sh $(TAXONOMY_DIR)new_taxdump/host.dmp $(PROTEIN)

clean:
	rm -f $(NUC)
	rm -f $(DEAD)
	rm -f $(PROTEIN)
