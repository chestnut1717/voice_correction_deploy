import numpy as np
import librosa
import matplotlib.pyplot as plt

# 그래프 디자인 담당 함수
def plot_design(ans_rms, deaf_rms, linewidth="4", smoothing=True):
      plt.figure(figsize=[20,9])
      plt.plot(ans_rms, color = "Blue",
                            linewidth = linewidth, 
                            label="Answer")
      plt.plot(deaf_rms, color = "Red",
                            linewidth = linewidth, 
                            label = "Yours")
      plt.axis('off')
      plt.legend(fontsize=30)

      if smoothing:
        filename = "graph_smoothing.png"
      else:
        filename = "graph_not_smoothing.png"
        
      plt.savefig("database/graph/" + filename, pad_inches=0)

# 사용자와 정답 목소리의 pitch 그래프화하는 함수
def to_graph(ans_wav, deaf_wav, smoothing=False):

    ans_rms, deaf_rms = librosa.feature.rms(ans_wav), librosa.feature.rms(deaf_wav)

    ans_new_rms, deaf_new_rms = downsample(ans_rms, deaf_rms)
    if smoothing == True:
      ans_rms_sm = moving_average(ans_new_rms, 10)
      deaf_rms_sm = moving_average(deaf_new_rms, 10)
      plot_design(ans_rms_sm, deaf_rms_sm, linewidth="4", smoothing=smoothing)

    else:
      plot_design(ans_rms, deaf_rms, linewidth="4", smoothing=smoothing)

    return None

# 그래프 평활화
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w


# 두 개의 다른 signal 길이 맞춰주는 함수 고안
def downsample(ans, deaf):
    pivot = 0
    ans, deaf = ans.flatten(), deaf.flatten()
    if len(ans) > len(deaf):
        target, compare = ans, deaf
    else:
        target, compare = deaf, ans
        pivot = 1

  # 정규화
    norm = np.linalg.norm(target)
    target = target/norm

    norm = np.linalg.norm(compare)
    compare = compare/norm

    sampled_list = []
    padding_size = int(len(target) / len(compare))
    print(padding_size)
    if padding_size > 1:
        for i in range(0, len(target), padding_size):
            tmp = np.mean( target[i:i+padding_size] )
            sampled_list.append(tmp)
    else:
        per = np.percentile(target, 100 - len(compare)/len(target)*100)
        print('percentile')
        print(len(compare)/len(target))
        print(per)
        target = np.array(target[(target > per)])

    # target is deaf
    if pivot == 1:
      return compare, target
    # compare is deaf
    else:
      return target, compare


# LCS 알고리즘을 사용하여 두 string 중에서 겹치는 음소 subsequence 출력 용도
def lcs_algo(S1, S2, m, n):
    L = [[0 for x in range(n+1)] for x in range(m+1)]

    # bottom-up 방식으로 matrix 쌇아감
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif S1[i-1] == S2[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    index = L[m][n]

    lcs_algo = [""] * (index+1)
    lcs_algo[index] = ""

    i = m
    j = n
    while i > 0 and j > 0:

        if S1[i-1] == S2[j-1]:
            lcs_algo[index-1] = S1[i-1]
            i -= 1
            j -= 1
            index -= 1

        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1
            
    #  subsequences 출력
    print("S1 : " + S1 + "\nS2 : " + S2)

    lcs = "".join(lcs_algo)
    print("LCS: " + lcs)

    return lcs

# 정확도 및 score 반환
def calculate_acc(ans, lcs):
    accuracy = int(len(lcs) / len(ans) * 100)
    score = ""

    if accuracy >= 90:
        score = "Perfect"
    elif accuracy >= 70:
        score = "Great"
    elif accuracy >= 50:
        score = "Good"
    else:
        score = "Try Again"

    return accuracy, score

# 장음기호(ː)연결시켜주는 프로그램
def long_vowel_process(phonemes):

  idx = 0
  new_phonemes = []

  while idx < len(phonemes):
    if (idx+1) < len(phonemes) and phonemes[idx + 1] == "ː":
      new_phonemes.append(phonemes[idx] + phonemes[idx + 1])
      idx += 2
    else:
      new_phonemes.append(phonemes[idx])
      idx += 1
  

  return new_phonemes

# 정답 음소와 발화자의 음소 중, 일치하는 음소 구분해서 출력해주는 함수
def highlight(ans, lcs):
  # answer phonemes중에 틀린것은 0, 일치하는 것은 1로 두어, 0인것은 나중에 틀린것 표시하기 위함

  new_ans = long_vowel_process(ans)
  new_lcs = long_vowel_process(lcs)

  correct = [[i, 0] for i in new_ans]
  idx=0

  # lcs에서 하니씩 음소를 가져와서 answer과 비교함
  ## 일치하면 correct의 해당 음소의 값을 0에서 1로
  for char in new_lcs:
      while idx < len(new_ans):
          tmp = new_ans[idx]

          if tmp == char:
              correct[idx][1] = 1
              idx += 1
              break
          idx += 1
    
  return correct

