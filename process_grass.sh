# Author: Gorgens, E. B.
# Pourpose: Process LiDAR transects and extract trees of interest

# 1 = NP_T-403
# 2 = t403
# 3 = 35
# 4 = 6

r.in.lidar -o -e --overwrite input=/home/gorgens/Documents/grassdata/INPE/d_universal/$1.las output=$2_min method=min resolution=1

g.region raster=$2_min@universal

r.neighbors --overwrite input=$2_min@universal output=$2_mdt method=min size=7
r.neighbors --overwrite input=$2_mdt@universal output=$2_mdt_v2 method=median size=11

r.in.lidar -o -e --overwrite input=/home/gorgens/Documents/grassdata/INPE/d_universal/$1.las output=$2_mds method=percentile pth=95 resolution=1

r.mapcalc "$2_chm = $2_mds@universal - $2_mdt_v2@universal" --overwrite

r.out.ascii --overwrite input=$2_chm@universal output=/home/gorgens/Documents/grassdata/INPE/d_universal/$2_chm precision=2 null_value=-9999

r.mapcalc "$2_topcanopy = if( $2_chm@universal < $3 , null()  , $2_chm@universal)" --overwrite
r.mapcalc "$2_topcanopyMask = if( $2_chm@universal < $3 , null()  , 1)" --overwrite
r.to.vect --overwrite input=$2_topcanopyMask@universal output=$2_topcanopy_vector type=area

v.db.addcolumn map=$2_topcanopy_vector@universal columns="area_m DOUBLE PRECISION"
v.to.db map=$2_topcanopy_vector@universal option=area columns=area_m units=meters

v.extract input=$2_topcanopy_vector@universal output=$2_topcanopy_vector6@universal where="area_m > $4"
