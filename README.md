# Remove_Annotation
## 註解剔除器

![Remove Annotation cover](https://github.com/zz22558822/Remove_Annotation/blob/main/img/Remove_Annotation.png)

---

## 前言
原先要去除註解都在 Visual Studio Code 使用 Ctrl + H 帶入下方的正則表達式替換為空
```
\/\*[\s\S]*?\*\/|(?<!http:|https:)\/\/[^\n]*(?![\s\S]*http:|[\s\S]*https:)|<!--[\s\S]*?-->|(?<!http:|https:)\/\/[^\n]*|^\s*\n

```
但是更改上還是不便利，還需要 Copy 後進行操作，故此有開發此程序的想法，
至於不使用進度條是因為一次性處理大量檔案(100+)的機會比較少應該沒有太大影響。

## 剔除說明

去除 C 的註解
```
\/\*[\s\S]*?\*\/
```
去除 JavaScript、Scss 的註解 (跳過http: 或 https:)
```
(?<!http:|https:)\/\/[^\n]*(?![\s\S]*http:|[\s\S]*https:)
```
去除 HTML 的註解
```
<!--[\s\S]*?-->
```
去除 Python 的註解 (# 較為易見，有依照副檔名判斷是否啟用)
```
\#.* 
```

## 使用方法:
1. 將需要替除註解的檔案們拖曳至 Remove_Annotation.exe
2. 找到拖曳的檔案路徑名稱 + min 即是剔除後的檔案
3. 檢查是否有特殊格式被處理，請閱讀下列注意事項

## 注意事項
本程序採用正則表達式作為剃除的依據，因此若有會被誤判的還須特別留意，例如:
```
r'\/\*[\s\S]*?\*\/|(?<!http:|https:)\/\/[^\n]*(?![\s\S]*http:|[\s\S]*https:)|<!--[\s\S]*?-->|(?<!http:|https:)\/\/[^\n]*'
```
此處會遭到刪減:
```
<!--[\s\S]*?-->
```

本程序編碼預設使用UTF-8，可自行更改，視情況更新自適應編碼

## 檔案結構
File/  
└── Remove_Annotation.exe → 主程序


---

## Releases 有打包完成的版本(建議使用)
