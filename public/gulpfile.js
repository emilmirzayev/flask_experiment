const {src, dest, watch, series, parallel} = require('gulp');
let sourcemaps = require('gulp-sourcemaps');
let sass = require("gulp-sass")(require("node-sass"));
let concat = require('gulp-concat');
let terser = require('gulp-terser');
let postcss = require('gulp-postcss');
let autoprefixer = require('autoprefixer');
let cssnano = require('cssnano');
let replace = require('gulp-replace');

const files = {
    scssPath: './scss/**/*.scss',
    jsPath: './scripts/*.js'
}

const scssTask = () => src(files.scssPath)
    .pipe(sourcemaps.init())
    .pipe(sass())
    .pipe(postcss([autoprefixer(), cssnano()]))
    .pipe(sourcemaps.write('.'))
    .pipe(dest('./public/assets/css/')
    );

const jsTask = () => src([
    './scripts/jquery-1.11.0.min.js',
    './scripts/jquery.mask.js',
    './scripts/jquery.dataTables.min.js',
    './scripts/tmpl.min.js',
    './scripts/scripts.js'])
    .pipe(sourcemaps.init())
    .pipe(concat('scripts.js'))
    .pipe(terser())
    .pipe(dest('./public/assets/js/')
    );

const cbString = new Date().getTime();
const cacheBustTask = () => src(['index.html'])
    .pipe(replace(/cb=\d+/g, 'cb=' + cbString))
    .pipe(dest('.'));

const watchTask = () => {
    watch([files.scssPath, files.jsPath],
        series(
            parallel(scssTask, jsTask),
            cacheBustTask
        )
    );
};

/*
 Develop once.
*/
const dev = parallel(scssTask, jsTask);

exports.watch = series(
    parallel(scssTask, jsTask),
    cacheBustTask,
    watchTask
);
exports.dev = dev;
