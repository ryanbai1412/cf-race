cd /home/ubuntu/repos/cf-race
for p in "$@"; do
  python3 pipeline/rated_pool.py archive --rating 1400 --target 100 --workspace ~/Documents/cf-pools --cache ~/.cache/cf-race-pool --id $p --output ~/Documents/w1400/arch8/rating1400-$p.tar.gz 2>&1 | tail -1
done
cd ~/Documents/w1400/arch8 && sha256sum *.tar.gz *.provenance.json > SHA256SUMS
