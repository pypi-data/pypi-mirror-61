# @Author: Tang Yubin <tangyubin>
# @Date:   2019-05-26T12:04:11+08:00
# @Email:  tang-yu-bin@qq.com
# @Last modified by:   tangyubin
# @Last modified time: 2019-05-26T16:24:35+08:00
import numpy as np
import pandas as pd

class DecisionTreeHelper():
    def __init__(self, estimator):
        self.estimator = estimator

    def get_decision_path_info(self, X):
        """
        获取样本在决策树中的决策路径
        :param dtc: 决策树模型（已经训练好的）
        :param X: 样本（只包含特征）
        :return: 每个样本在决策树种的决策路径
        """
        feature = self.estimator.tree_.feature

        threshold = self.estimator.tree_.threshold
        leave_id = self.estimator.apply(X)
        node_indicator = self.estimator.decision_path(X)
        path_info_list = []
        for i in range(X.shape[0]):
            path_info = dict()
            path_info['features_in_path'] = []
            path_info['threshold_in_path'] = []
            path_info['feature_values_in_path'] = []
            path_info['threshold_sign_in_path'] = []

            node_index = node_indicator.indices[node_indicator.indptr[i]:node_indicator.indptr[i + 1]]
            for node_id in node_index:
                if leave_id[i] == node_id:
                    path_info['n_samples_of_class'] = self.estimator.tree_.value[node_id][0]
                    path_info['class'] = np.argmax(self.estimator.tree_.value[node_id][0])
                    continue
                if X[i, feature[node_id]] <= threshold[node_id]:
                    threshold_sign = "<="
                else:
                    threshold_sign = ">"
                path_info['features_in_path'].append(feature[node_id])
                path_info['threshold_in_path'].append(threshold[node_id])
                path_info['feature_values_in_path'].append(X[i, feature[node_id]])
                path_info['threshold_sign_in_path'].append(threshold_sign)
            path_info_list.append(path_info)
        return path_info_list

    def print_decision_path(self, path_info, feature_names):
        """
        打印一条决策路径的信息
        :param path_info: 决策路径 Dict
        :param feature_names: 特征名称列表
        :return:
        """
        print("Rules to predict sample:")
        print("---------------")
        infos = [path_info['features_in_path'], path_info['threshold_in_path'],
                 path_info['feature_values_in_path'], path_info['threshold_sign_in_path']]
        for i, (feature, threshold, value, sign) in enumerate(zip(*infos)):
            print("rule {} : value of {}  is {}, threshold = {:.2}, value of sample's feature {} threshold.".format(
                i, feature_names[feature], value, threshold, sign))

        print("\n\n number of every class's samples which fit above rules:")
        print('---------------')
        for i, num in enumerate(path_info['n_samples_of_class']):
            print("class {} : {}".format(i, num))

        print("\n\n Decision result :")
        print('---------------')
        print("the most class is {}, so all the samples in the leaf node are labeled {}".format(
            path_info['class'], path_info['class']))

    def find_similar_instance(self, instance, candidate):
        """
        在候选样例中找出与当前样落本在决策树中同一个叶子节点里的样本
        :param instance:
        :param candidate:
        :return:
        """
        leaf_id = self.estimator.apply(instance)[0]
        leave_id = self.estimator.apply(candidate)
        return np.argwhere(leave_id == leaf_id)

    def get_samples_of_leaf(self, leaf_id, X):
        leaves_id = self.estimator.apply(X)
        return np.argwhere(leaves_id == leaf_id)

    def get_decision_path_of_leaf(self, leaf_id):
        pass

    def get_tree_info(self):
        """
        获取一棵决策树的信息
        :return: Dict('depth':depth, 'n_leaves':n_leaves, 'leaves':DataFrame('node_id':node_id,
                'parent_depth':parent_depth, 'n_samples_of_class_x':n_samples, 'class':class))
        """
        tree_info = dict()
        tree_info['depth'] = self.estimator.get_depth()
        tree_info['n_leaves'] = self.estimator.get_n_leaves()
        # 获取每个叶子节点的信息（所属类别，各种类别的样本分布情况）
        n_nodes = self.estimator.tree_.node_count
        children_left = self.estimator.tree_.children_left
        children_right = self.estimator.tree_.children_right
        node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
        stack = [(0, -1)]
        leaves_info = []
        while len(stack) > 0:
            node_id, parent_depth = stack.pop()
            node_depth[node_id] = parent_depth + 1
            if children_left[node_id] != children_right[node_id]:
                stack.append((children_left[node_id], parent_depth + 1))
                stack.append((children_right[node_id], parent_depth + 1))
            else:
                leaf_info = dict()
                leaf_info['node_id'] = node_id
                leaf_info['parent_depth'] = parent_depth
                for i in range(self.estimator.tree_.value[node_id][0].shape[0]):
                    leaf_info['n_samples_of_class_{}'.format(i)] = self.estimator.tree_.value[node_id][0][i]
                leaf_info['class'] = np.argmax(self.estimator.tree_.value[node_id][0]) # cls_id
                leaves_info.append(leaf_info)
        df_leaves = pd.DataFrame(data=leaves_info)
        tree_info['leaves'] = df_leaves
        return tree_info
