<template>
    <div class="fixed h-screen w-auto z-10 top-5 left-0 overflow-x-visible overflow-y-scroll bg-black my-5 px-2 leading-7" v-if="navigationStore.showChapterNav">
        <a href="#" onclick="load('chapters/home.html');">Home</a><br>
        <a href="#" onclick="load('chapters/preface.html');">Preface</a><br>
        <a href="#" @click="chapterStore.changeChapter(1)">Chapter 1</a><br>
        <a href="#" onclick="load('chapters/chapter2.html');">Chapter 2</a><br>
        <a href="#" onclick="load('chapters/chapter3.html');">Chapter 3</a><br>
        <a href="#" onclick="load('chapters/chapter4.html');">Chapter 4</a><br>
        <a href="#" onclick="load('chapters/chapter5.html');">Chapter 5</a><br>
        <a href="#" onclick="load('chapters/chapter6.html');">Chapter 6</a><br>
        <a href="#" onclick="load('chapters/chapter7.html');">Chapter 7</a><br>
        <a href="#" onclick="load('chapters/chapter8.html');">Chapter 8</a><br>
        <a href="#" onclick="load('chapters/chapter9.html');">Chapter 9</a><br>
        <a href="#" onclick="load('chapters/chapter10.html');">Chapter 10</a><br>
        <a href="#" onclick="load('chapters/chapter11.html');">Chapter 11</a><br>
        <a href="#" onclick="load('chapters/chapter12.html');">Chapter 12</a><br>
        <a href="#" onclick="load('chapters/chapter13.html');">Chapter 13</a><br>
        <a href="#" onclick="load('chapters/chapter14.html');">Chapter 14</a><br>
        <a href="#" onclick="load('chapters/chapter15.html');">Chapter 15</a><br>
        <a href="#" onclick="load('chapters/chapter16.html');">Chapter 16</a><br>
        <a href="#" onclick="load('chapters/chapter17.html');">Chapter 17</a><br>
        <a href="#" onclick="load('chapters/chapter18.html');">Chapter 18</a><br>
        <a href="#" onclick="load('chapters/chapter19.html');">Chapter 19</a><br>
        <a href="#" onclick="load('chapters/chapter20.html');">Chapter 20</a><br>
        <a href="#" onclick="load('chapters/chapter21.html');">Chapter 21</a><br>
        <a href="#" onclick="load('chapters/chapter22.html');">Chapter 22</a><br>
        <a href="#" onclick="load('chapters/chapter23.html');">Chapter 23</a><br>
        <a href="#" onclick="load('chapters/chapter24.html');">Chapter 24</a><br>
        <a href="#" onclick="load('chapters/chapter25.html');">Chapter 25</a><br>
        <a href="#" onclick="load('chapters/chapter26.html');">Chapter 26</a><br>
        <a href="#" onclick="load('chapters/chapter27.html');">Chapter 27</a><br>
        <a href="#" onclick="load('chapters/chapter28.html');">Chapter 28</a><br>
        <a href="#" onclick="load('chapters/chapter29.html');">Chapter 29</a><br>
        <a href="#" onclick="load('chapters/chapter30.html');">Chapter 30</a><br>
        <a href="#" onclick="load('chapters/chapter31.html');">Chapter 31</a><br>
        <a href="#" onclick="load('chapters/chapter32.html');">Chapter 32</a><br>
        <a href="#" onclick="load('chapters/chapter33.html');">Chapter 33</a><br>
        <a href="#" onclick="load('chapters/chapter34.html');">Chapter 34</a><br>
        <a href="#" onclick="load('chapters/chapter35.html');">Chapter 35</a><br>
        <a href="#" onclick="load('chapters/chapter36.html');">Chapter 36</a><br>
        <a href="#" onclick="load('chapters/chapter37.html');">Chapter 37</a><br>
        <a href="#" onclick="load('chapters/chapter38.html');">Chapter 38</a><br>
        <a href="#" onclick="load('chapters/chapter39.html');">Chapter 39</a><br>
        <a href="#" onclick="load('chapters/chapter40.html');">Chapter 40</a><br>
        <a href="#" onclick="load('chapters/chapter41.html');">Chapter 41</a><br>
        <a href="#" onclick="load('chapters/chapter42.html');">Chapter 42</a><br>
        <a href="#" onclick="load('chapters/chapter43.html');">Chapter 43</a><br>
        <a href="#" onclick="load('chapters/chapter44.html');">Chapter 44</a><br>
        <a href="#" onclick="load('chapters/chapter45.html');">Chapter 45</a><br>
        <a href="#" onclick="load('chapters/chapter46.html');">Chapter 46</a><br>
        <a href="#" onclick="load('chapters/chapter47.html');">Chapter 47</a><br>
        <a href="#" onclick="load('chapters/chapter48.html');">Chapter 48</a><br>
        <a href="#" onclick="load('chapters/chapter49.html');">Chapter 49</a><br>
        <a href="#" onclick="load('chapters/chapter50.html');">Chapter 50</a><br>
    </div>
</template>

<script setup>
import { useNavigationStore } from '@/store/index'
import { useChapterStore } from '@/store/chapter'
const navigationStore = useNavigationStore()
const chapterStore = useChapterStore()
</script>
