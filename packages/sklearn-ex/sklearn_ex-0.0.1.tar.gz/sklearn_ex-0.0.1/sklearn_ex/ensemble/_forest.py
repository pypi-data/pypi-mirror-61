import numpy as np
import pandas as pd
from ..tree import DecisionTreeHelper


class RandomForestHelper():
    def __init__(self, estimator):
        self.estimator = estimator

    def get_similar_samples(self, samples, candidates, top_k, verbose=0):
        """
        对一组样本中的每个样本，在另一组样本中找出最相似的k个样本，依据在随机森林中落到同一个叶子节点的数量来衡量相似性。
        :param samples: 要处理的一组样本
        :param candidates: 寻找相似样本的一组样本
        :param top_k: 前k个最相似的
        :param verbose: 是否打印处理过程
        :return: 最相似的k个样本在candidates中的下标，相似样本在多少棵决策树中落到了同一个叶子节点。
        """
        sample_leaves = self.estimator.apply(samples)
        candidate_leaves = self.estimator.apply(candidates)
        top_k_idx_list = []
        top_k_num_list = []
        for i in range(sample_leaves.shape[0]):
            if verbose > 0 and i % 100 == 0:
                print('processing {} ...'.format(i))
            like_arr = (candidate_leaves == sample_leaves[i:i+1, :])
            sum_like_arr = like_arr.sum(axis=1)
            top_k_idxs = sum_like_arr.argsort().tolist()[-top_k:]
            top_k_idxs.reverse()
            tok_k_idx_list.append(top_K_idxs)
            top_k_num_list.append(sum_like_arr[top_k_idxs].tolist())
        return top_k_idx_list, top_k_num_list

    def get_forest_info(self):
        trees_info = []
        leaves_info = []
        for i, tree in enumerate(self.estimator.estimators_):
            helper = DecisionTreeHelper(tree)
            tree_info = helper.get_tree_info()
            leaves_info.append(tree_info.pop('leaves'))
            tree_info['tree_id'] = i
            trees_info.append(tree_info)
        df_trees_info = pd.DataFrame(data=trees_info)
        return df_trees_info, leaves_info


